import sys
import os
import os.path

data_folder=sys.argv[1]

def Folder_walk():
    path = sys.argv[1]
    #print(path)
    if len(sys.argv) < 2:
        print("Input the path file")
        exit(1)
    if os.path.isfile(path):
        Analyze(path)
    else:
        contents = os.listdir(path) # read the contents of dir
        for item in contents:      # loop over those contents
                Analyze(item) 

def Analyze(path):    
    #print(path)
    if ".py" in path:
        c_check(path)
    if ".asm" in path:
        asm_check(path)    


def asm_check(path):
    line_no = 1
    keyword=["printf","sprintf","strcpy","push"]
    with open(path, 'r') as f:
        for line in f:
            for i in keyword:
                if i in line:
                    print(line_no,i)
            line_no+=1 

def c_check(path):
    #print(path)
    keyword=["printf", "sprintf", "strcpy", "gets", "fgets", "puts", "execlp", "system", "strcpy",
                             "strcmp","execvp", "File", "sleep", "memcpy","strncat" ,"scanf", "push"]
    dict={
         "printf":"Overflowing Function vulnerability",
         "sprintf":"Overflowing Function vulnerability",
         "strcpy":"Buffer overflow vulnerablity",
         "gets":"Overflowing Function vulnerability", 
         "fgets":"Overflowing Function Vulnerability",
         "puts":"Overflowing Function Vulnerability",
         "execlp":"Path Vulnerability", 
         "system":"Command injection Vulnerablity", 
         "strcmp":"Buffer overflow Vulnerability",
         "execvp":"Path Vulnerability",
         "File":"Function Vulnerablitiy",
         "sleep":"Function Vulnerablity",
         "memcpy":"Buffer Overflow Vulnerability",
         "strncat":"Dot Dot vulnerablity",
         "scanf":"Overflowing Function Vulnerability",
         "push":"Stack Vulnerability"
    }
    #print("Hello") 
    line_no = 1
    #print(folder)
    if os.path.isfile(path):
        file_to_open = path
    else: 
        file_to_open = os.path.join(data_folder, path)
    print(file_to_open)
    with open(file_to_open) as f:
        for line in f:
            for i in keyword:
                if i in line:
                    print("Given file, line number {n} found {s} -------->{t}".format(n=line_no,s=i,t=dict[i]))
            line_no+=1        
            

Folder_walk()