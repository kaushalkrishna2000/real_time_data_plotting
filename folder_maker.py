import os

print(os.environ.get("USER_TR"),os.environ.get("FOLDER_TR"))

folder=os.environ.get("FOLDER_TR",'trial_1')

folder_path=folder+"/"

os.system(f"mkdir {folder} ")
os.system(f"mkdir {folder_path}csv")
os.system(f"mkdir {folder_path}log")
os.system(f"mkdir {folder_path}jpg")