class MetaData:
    """
    Parameters:
    - submitted_by_name (str) - Name of steward entering data
    - submitted_by_email (str) - Email of steward entering data
    - tag_shape (bool) - Tag shape. True for circle, False for Rectangle.
    - tag_number (int) - The ORS tag number.
    - measurement_url (str | None) - Optional. The sheet url in the "Entered into Master Sheet" drive folder.
    - monitoring_date (str) - Monitoring date of ORS survey (MM/DD/YYYY)
    - primary_steward (str) - Name of primary steward.
    - primary_steward_email (str) - Email of primary steward.
    - number_of_adults_monitoring (int) - Number of adults monitoring
    - number_of_students_monitoring (int) - Number of students monitoring
    - location (str) - Location of monitoring. Example: "Battery Park"
    - avg_shell_height (int) - The average shell height within the survey
    - organization (str) - Affiliation with BOP. Example: "Ambassador" "Community Scientist"
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
                 submitted_by_name: str | None = None,
                 submitted_by_email: str | None = None,
                 tag_shape: int | None = None,
                 tag_number: int | None = None,
                 monitoring_date: str | None = None,
                 primary_steward: str | None = None,
                 primary_steward_email: str | None = None,
                 location: str | None = None,
                 avg_shell_height: int | None = None,
                 organization: str | None = None,
                 total_live_oysters: int | None = None,
                 total_live_oysters_geq_15mm: int | None = None,
                 total_live_oysters_lt_15mm: int | None = None,
                 total_dead_oysters_geq_15mm: int | None = None,
                 total_dead_oysters_lt_15mm: int | None = None,
                 measurement_url: str | None = None,
                 broodstock: str | None = None,
                 set_date: str | None = None,
                 distribution_date: str | None = None,
                 number_of_adults_monitoring: int | None = None,
                 number_of_students_monitoring: int | None = None
                ):
        self.submitted_by_name = submitted_by_name # prompt
        self.submitted_by_email = submitted_by_email # prompt
        self.tag_shape = tag_shape # prompt
        self.tag_number = tag_number # prompt
        self.monitoring_date = monitoring_date # prompt
        self.primary_steward = primary_steward # prompt
        self.primary_steward_email = primary_steward_email  # prompt
        self.number_of_adults_monitoring = number_of_adults_monitoring # prompt
        self.number_of_students_monitoring = number_of_students_monitoring # prompt
        self.location = location # prompt
        self.avg_shell_height = avg_shell_height
        self.organization = organization # prompt
        self.total_live_oysters = total_live_oysters
        self.total_live_oysters_geq_15mm = total_live_oysters_geq_15mm
        self.total_live_oysters_lt_15mm = total_live_oysters_lt_15mm
        self.total_dead_oysters_geq_15mm = total_dead_oysters_geq_15mm
        self.total_dead_oysters_lt_15mm = total_dead_oysters_lt_15mm
        self.measurement_sheet_url = measurement_url
        self.broodstock = broodstock # prompt
        self.set_date = set_date # prompt 
        self.distribution_date = distribution_date # prompt

    def prompt_metadata(self):
        self.submitted_by_name = input("(Step 1 of 14) Name: ")
        self.submitted_by_email = input("(Step 2 of 14) Email: ")
        self.tag_shape = int(input("(Step 3 of 14) Tag Shape (0 for circle 1 for square): "))
        self.tag_number = int(input("(Step 4 of 14) Tag Number: "))
        self.monitoring_date = input("(Step 5 of 14) Monitoring Data (MM/DD/YYYY): ")
        self.primary_steward = input("(Step 6 of 14) Primary Steward Name: ")
        self.primary_steward_email = input("(Step 7 of 14) Primary Steward Email: ")
        self.number_of_adults_monitoring = int(input("(Step 8 of 14) Number of adults monitoring: "))
        self.number_of_students_monitoring = int(input("(Step 9 of 14) Number of students monitoring: "))
        self.location = input("(Step 10 of 14) Name of site: ")
        self.organization = input("(Step 11 of 14) Affiliation of steward (e.g. Ambassador): ")
        self.broodstock = input("(Step 12 of 14) Broodstock (e.g MB): ")
        self.set_date = input("(Step 13 of 14) Cage set date (MM/DD/YYYY): ")
        self.distribution_date = input("(Step 14 of 14) Cage distribution date (MM/DD/YYYY): ")