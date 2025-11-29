import sys
import os
sys.path.append(os.getcwd())

print("Importing reactions...")
try:
    import reactions
    print("reactions imported successfully.")
except Exception as e:
    print(f"Error importing reactions: {e}")

print("Importing simulate...")
try:
    import simulate
    print("simulate imported successfully.")
except Exception as e:
    print(f"Error importing simulate: {e}")

print("Importing visualize...")
try:
    import visualize
    print("visualize imported successfully.")
except Exception as e:
    print(f"Error importing visualize: {e}")

print("Importing gui...")
try:
    import gui
    print("gui imported successfully.")
except Exception as e:
    print(f"Error importing gui: {e}")
