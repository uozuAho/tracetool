tracetool
=========

Simple tracing tool intended for embedded/low level systems.


requirements
------------
- free
- no embedded OS required
- some target resident code required
-- can be enabled/disabled at compile time, similar to logging
- user-specified data format
- customisable python-based analysis software

limitations
-----------
- intrusive (requires tracing code on embedded target)
- no host control (host just logs & displays)

alternatives/inspirations
-------------------------
http://micrium.com/tools/ucprobe/overview/ (not free)
https://lttng.org/ (linux only)
http://www.mentor.com/embedded-software/sourcery-tools/sourcery-analyzer/ (linux only)
ARM ETM ETB - over my head
