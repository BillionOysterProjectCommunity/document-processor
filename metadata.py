class MetaData:
    """
    Parameters:

    - tag_shape (bool) - Tag shape. True for circle, False for Rectangle.
    - tag_number (int) - The ORS tag number.
    - measurement_url (str | None) - Optional. The sheet url in the "Entered into Master Sheet" drive folder.
    - monitoring_date (str) - Monitoring date of ORS survey (MM/DD/YYYY)
    - total_live_oysters (int) - Total number of live oysters
    - total_live_oysters_geq_15mm (int) - Total number of live oysters >= 15mm
    - total_live_oysters_lt_15mm (int) - Total number of live oysters < 15mm
    - total_dead_oysters_geq_15mm (int) - Total number of dead oysters >= 15mm
    - total_dead_oysters_lt_15mm (int) - Total number of dead oysters < 15mm
    - broodstock (str) - Cage broodstock identifier
    - set_date (str) - Cage set date
    - distribution_date (str) - Cage distribution date

    """
    def __init__(self,
                 tag_shape: bool,
                 tag_number: int,
                 monitoring_date: str,
                 total_live_oysters: int,
                 total_live_oysters_geq_15mm: int,
                 total_live_oysters_lt_15mm: int,
                 total_dead_oysters_geq_15mm: int,
                 total_dead_oysters_lt_15mm: int,
                 measurement_url: str | None = None,
                 broodstock: str | None = None,
                 set_date: str | None = None,
                 distribution_date : str | None = None,
                ):
        self.tag_shape = tag_shape
        self.tag_number = tag_number
        self.monitoring_date = monitoring_date
        self.total_live_oysters = total_live_oysters
        self.total_live_oysters_geq_15mm = total_live_oysters_geq_15mm
        self.total_live_oysters_lt_15mm = total_live_oysters_lt_15mm
        self.total_dead_oysters_geq_15mm = total_dead_oysters_geq_15mm
        self.total_dead_oysters_lt_15mm = total_dead_oysters_lt_15mm
        self.measurement_sheet_url = measurement_url
        self.broodstock = broodstock
        self.set_date = set_date
        self.distribution_date = distribution_date
