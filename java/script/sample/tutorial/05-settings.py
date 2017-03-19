from soda import *

settings.mode = FeedbackModes.normal

Phase("External calls",
    Call("echo foobar")
).do()

settings.mode = FeedbackModes.quiet

Phase("External calls",
    Call("echo foobar")
).do()

settings.mode = FeedbackModes.silent

Phase("External calls",
    Call("echo foobar")
).do()