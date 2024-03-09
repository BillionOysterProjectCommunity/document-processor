from typing import List, Sequence

from theia.settings.config import config
import theia.utils.filters as filter

from google.cloud import documentai_v1 as documentai
import pandas as pd
import numpy as np

DOCUMENT_CLIENT_CONFIG = "documentai"

class DocumentProcessor():
    def __init__(self):
        pass

    def text_anchor_to_text(self, text_anchor: documentai.Document.TextAnchor, text: str) -> str:
        """
        Document AI identifies table data by their offsets in the entirety of the
        document's text. This function converts offsets to a string.
        """
        response = ""
        # If a text segment spans several lines, it will
        # be stored in different text segments.
        for segment in text_anchor.text_segments:
            start_index = int(segment.start_index)
            end_index = int(segment.end_index)
            response += text[start_index:end_index]
        return response.strip().replace("\n", " ")

    def get_table_data(
        self, rows: Sequence[documentai.Document.Page.Table.TableRow], text: str
    ) -> List[List[str]]:
        """
        Get Text data from table rows
        """
        all_values: List[List[str]] = []
        for row in rows:
            current_row_values: List[str] = []
            for cell in row.cells:
                current_row_values.append(
                    self.text_anchor_to_text(cell.layout.text_anchor, text)
                )
            all_values.append(current_row_values)
        return all_values
    
    def proccess_table(self, document: documentai.Document) -> List[pd.DataFrame]:

        tables = []

        header_row_values: List[List[str]] = []
        body_row_values: List[List[str]] = []

        for page in document.pages:
            for index, table in enumerate(page.tables):
                header_row_values = self.get_table_data(table.header_rows, document.text)
                body_row_values = self.get_table_data(table.body_rows, document.text)

                # Create a Pandas Dataframe to print the values in tabular format.
                df = pd.DataFrame(
                    data=body_row_values,
                    columns=pd.MultiIndex.from_arrays(header_row_values),
                )
                
                tables.append(df)

        return tables
    
    def process_columns(self, table: pd.DataFrame):
    
        columns = {"measurements": [], "live_dead": []}
        
        for column in table.columns:
            if column[0] != '':
                if "MEASUREMENT" in column[0]:
                    columns["measurements"].append(column)
                if "Live" in column[0] or "Dead" in column[0]:
                    columns["live_dead"].append(column)

        return columns
    
    def process_measurements(self, df: pd.DataFrame, columns) -> pd.DataFrame:
        
        m = np.array([filter.truncate(df[x].values) for x in columns["measurements"]]).flatten()
        ld = ld = np.array([filter.truncate(df[x].values) for x in columns["live_dead"]]).flatten()

        df = pd.DataFrame({"measurements": m, "live/dead": ld})

        df["measurements"] = df["measurements"].apply(lambda x: filter.filter_nums(x))
        df["live/dead"] = df["live/dead"].apply(lambda x: filter.filter_strings(x))

        return df
    
    def online_process(
            self, 
            file_path,
            project_id,
            processor_id,
            location,
        ) -> documentai.Document:
        """
        Processes a document using the Document AI Online Processing API.
        """
        # Refer to https://cloud.google.com/document-ai/docs/processors-list
        # for supported file types

        mime_type = "image/jpeg"
        
        opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}

        # Instantiates a client
        documentai_client = documentai.DocumentProcessorServiceClient(client_options=opts)

        # The full resource name of the processor, e.g.:
        # projects/project-id/locations/location/processor/processor-id
        # You must create new processors in the Cloud Console first
        resource_name = documentai_client.processor_path(project_id, location, processor_id)

        # Read the file into memory
        with open(file_path, "rb") as image:
            image_content = image.read()

            # Load Binary Data into Document AI RawDocument Object
            raw_document = documentai.RawDocument(
                content=image_content, mime_type=mime_type
            )

            # Configure the process request
            request = documentai.ProcessRequest(
                name=resource_name, raw_document=raw_document
            )

            # Use the Document AI client to process the sample form
            result = documentai_client.process_document(request=request)

            return result.document
        
    def process_document(
            self, 
            file_path,
        ):

        location = config(key='location')
        project_id = config(key='project-id')
        processor_id = config(key='processor-id')

        document = self.online_process(file_path, project_id, processor_id, location)
        tables = self.proccess_table(document)
        df = tables[0] # The 0th table is the front page of a standard ORS document
        columns = self.process_columns(df)
        measurements = self.process_measurements(df, columns)

        return measurements
