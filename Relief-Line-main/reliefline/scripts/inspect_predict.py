import importlib, os, sys, inspect
p = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', 'ml', 'predict.py'))
print('path:', p)
print('exists:', os.path.exists(p))
print('size:', os.path.getsize(p) if os.path.exists(p) else 'no file')
print('\n--- FILE HEAD (200 bytes) ---')
with open(p, 'rb') as f:
    print(f.read(200))
print('\n--- IMPORT MODULE ---')
try:
    m = importlib.import_module('app.ml.predict')
    print('module file:', getattr(m, '__file__', None))
    names = sorted([n for n in m.__dict__.keys() if not n.startswith('__')])
    print('names count:', len(names))
    print('names:', names)
    print('\n--- SOURCE via inspect ---')
    print(inspect.getsource(m))
except Exception as e:
    import traceback
    traceback.print_exc()
