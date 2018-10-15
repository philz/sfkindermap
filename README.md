# SF Public Elementary School Commute Sorter

This tool produces a tab-separated output modelling the
commute to every elementary school in SF. The two
options it emulates are:
  * (Transit) home to school; school to work
  * (Driving) home to school; school to home; (Transit) home to work
Your individual commute scenarios may vary, but this approach
makes sense if you currently take transit into downtown.

To run this, you need to acquire a Google Maps API key via
https://cloud.google.com/maps-platform/ (GetStarted, then Routes).  Running
this will incur about $10 on your credit card.

The list of elemntary schools is from page 28 of http://www.sfusd.edu/en/assets/sfusd-staff/enroll/files/2019-20/2019-20_enrollment_guide_ENG_FINAL_web.pdf
via cut and paste.
