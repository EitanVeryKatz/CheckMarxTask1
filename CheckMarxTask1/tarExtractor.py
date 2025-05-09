import ast
from doctest import debug_script
from msilib.schema import File
import ast
import tarfile
import os
import sys
import toml

def extractTarball(i_filepath, i_extract_to):
    try:
        print("began extraction process")
        limitedPathLengthsOS = ("win32","win64")
        if sys.platform in limitedPathLengthsOS:
            i_extract_to = os.path.abspath(i_extract_to)
            if not i_extract_to.startswith("\\\\?\\"):
                i_extract_to = f"\\\\?\\{i_extract_to}"
                

        with tarfile.open(i_filepath, "r:gz") as tar:
            tar.extractall(path=i_extract_to)
        print(f"Extracted to {i_extract_to}")
        return True
    
    except Exception as exceptionMessage:
        print(f"Failed to extract tarball: {exceptionMessage}")
        return False


def findDependencyFiles(i_extractPath):
    
    potentialFiles = ["setup.py", "pyproject.toml", "requirements.txt"]
    found = {}

    for root, dirs, files in os.walk(i_extractPath):
        for name in potentialFiles:
            if name in files:
                full_path = os.path.join(root, name)
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    found[name] = f.read()
                    print(f"Found {name} in {full_path}")
                    
    for fileName in potentialFiles:
        if fileName not in found:
            print(f"{fileName} not found")
            
    return parseRequirements(found)


#get list of all dependancies   
def parseRequirements(i_requirements):
    dependencies = []
    for fileName, fileContent in i_requirements.items():
        if fileName == "setup.py":
            ParseSetupPy(fileContent,dependencies)
                
        elif fileName == "pyproject.toml":
            # Parse pyproject.toml for dependencies
            parse_pyproject_toml(fileContent,dependencies)  
        elif fileName == "requirements.txt":
            # Parse requirements.txt for dependencies
            lines = fileContent.splitlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith("#"):
                    dependencies.append(line)
    for item in dependencies:
        print(f"Found dependency: {item}")
    print(f"Dependencies found: {dependencies}")
    return dependencies



def ParseSetupPy(i_setupPy,dependancies):
    
    class SetupVisitor(ast.NodeVisitor):
        
        def visit_Call(self, node):
            if isinstance(node.func, ast.Name) and node.func.id == "setup":
                for keyword in node.keywords:
                    if "require" in keyword.arg:
                        if isinstance(keyword.value, ast.List) or isinstance(keyword.value, ast.Tuple) or isinstance(keyword.value, ast.Dict):
                            for item in keyword.value.values:
                                if isinstance(item, ast.Str):  # For Python <3.8
                                    string_value = item.s
                                    dependancies.append(string_value)
                                    print(f"added dependancy{string_value}")
                                elif isinstance(item, ast.Constant) and isinstance(item.value, str):
                                    string_value = item.value
                                    dependancies.append(string_value)
                                    print(f"added dependancy{string_value}")
                                
            self.generic_visit(node)

    tree = ast.parse(i_setupPy)
    visitor = SetupVisitor()
    visitor.visit(tree)
    return 




def parse_pyproject_toml(path,dependancies):
    try:
        data = toml.loads(path)
        if "build-system" in data and "requires" in data["build-system"]:
            for item in data["build-system"]["requires"]:
                if isinstance(item, str):
                    dependancies.append(item)
                    print(f"added dependancy{item}")
    except Exception as e:
        print(f"Error parsing pyproject.toml: {e}")
        