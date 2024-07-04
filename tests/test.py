everything = 5

from time import sleep, time
from some_package_that_exports_everything import everything as most_things
import some_package_that_has_everything
from everything import export_from_everything_1, unused_export_from_everything
import everything

# everything

sleep(2)
time()

some_package_that_has_everything.everything
some_package_that_has_everything.everything()

everything

export_from_everything_1
export_from_everything_1()

everything.export_from_everything2
everything.export_from_everything2()

time.everything.this_is_not_an_everything_export()
