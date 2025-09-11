# Entry type constants
OFF_DAY = 'OD'
HALF_DAY = 'HD'
REGULAR_DAY = 'RH'


ENTRY_TYPE = (
    (REGULAR_DAY, 'Regular hours'),
    ('H', 'Holiday'),
    ('SL', 'Sick Leave'),
    ('AL', 'Annual Leave'),
    ('FH', 'Feeding Hour'),
    ('ML', 'Maternity Leave'),
    ('PL', 'Paternity Leave'),
    ('STL', 'Study Leave'),
    ('CL', 'Compassionate Leave'),
    (OFF_DAY, 'Off Day'),
    (HALF_DAY, 'Half Day'),
    ('WE', 'Weekend'))

STATUS = (
    ('draft', 'Draft'),
    ('new', 'New'),
    ('submitted', 'Submitted'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('verified', 'Verified'))
