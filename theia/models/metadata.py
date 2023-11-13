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

    def get_broodstock(self):
        """
        Returns the cage broodstock from ORS Sites and Stewards
        """
        # NOTE When searching broodstock prioritize column Q to N in ORS Sites and Stewards
        #      As column Q represents the MOST RECENT broodstock installation date.
        #      If column Q is present return the broodstock in column Q over the data point in N.
        #      (N = 1. Broodstock source) (Q = 2. Broodstock Source)

        return "WIP"
    
    def get_setDate(self):
        return "WIP"
    
    def get_distributionDate(self):
        return "WIP"

