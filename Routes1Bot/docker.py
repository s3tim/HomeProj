from googletrans import Translator
import inspect
print(inspect.iscoroutinefunction(Translator().translate))