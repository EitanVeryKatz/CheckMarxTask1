import os
import ast
import toml

def findDependencyFiles(i_extractPath):
    potentialFiles = {"setup.py", "pyproject.toml", "requirements.txt"}
    found = {}
    metadata_path = None

    for root, dirs, files in os.walk(i_extractPath):
        for name in potentialFiles:
            if name in files:
                full_path = os.path.join(root, name)
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    found[name] = f.read()
                    print(f"Found item {name} in {full_path}")
                    
        for dirname in dirs:
            if dirname.endswith(".dist-info"):
                candidate = os.path.join(root, dirname, "METADATA")
                if os.path.isfile(candidate):
                    metadata_path = candidate
                    break 
                
    if metadata_path:
        try:
            with open(metadata_path, "r", encoding="utf-8", errors="ignore") as f:
                found["METADATA"] = f.read()
                print(f"Found item METADATA in {metadata_path}")
        except Exception as e:
            print(f"Failed to read METADATA in {metadata_path}: {e}")
    

  
    for fileName in potentialFiles:
        if fileName not in found:
            print(f"{fileName} not found")

    return parseRequirements(found)



#get list of all dependancies   
def parseRequirements(i_requirements):
    dependencies = []
    
    # Check if any of the files are present
    for fileName, fileContent in i_requirements.items():
        if fileName == "setup.py":
            ParseSetupPy(fileContent,dependencies)
        elif fileName == "pyproject.toml":
            # Parse pyproject.toml for dependencies
            parse_pyproject_toml(fileContent,dependencies)  
        elif fileName == "requirements.txt":
            # Parse requirements.txt for dependencies
            parse_requirements_txt(fileContent,dependencies)
        elif fileName == "METADATA":
            # Parse METADATA for dependencies
            parse_metadata_file(fileContent,dependencies)
            
    # Remove duplicates
    dependencies = list(set(dependencies))
    
    
    return dependencies



def parse_requirements_txt(fileContent, dependancies):
    lines = fileContent.splitlines()
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            dependancies.append(line)
            print(f"added dependancy {line} from requirements.txt")
    return None

def parse_metadata_file(fileContent, dependencies):
    lines = fileContent.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("Requires-Dist:"):
            dep = line[len("Requires-Dist:"):].strip()
            dependencies.append(dep)
            print(f"added dependency {dep} from METADATA")


def ParseSetupPy(i_setupPy,dependancies):
    
    class SetupVisitor(ast.NodeVisitor):
        
        def visit_Call(self, node):
            if isinstance(node.func, ast.Name) and node.func.id == "setup":
                for keyword in node.keywords:
                    if keyword.arg and "require" in keyword.arg:
                        if isinstance(keyword.value, ast.Dict):
                            for item in keyword.value.values:
                                searchDependenciesInAstObject(item, dependancies)
                        elif isinstance(keyword.value, ast.List):
                            for item in keyword.value.elts:
                                searchDependenciesInAstObject(item, dependancies)


                                
            self.generic_visit(node)

    tree = ast.parse(i_setupPy)
    try:
         visitor = SetupVisitor()
         visitor.visit(tree)
    except Exception as e:
        print(f"Error parsing setup.py: {e}")
        
    return None



def parse_pyproject_toml(path,dependancies):
    try:
        data = toml.loads(path)
        if "build-system" in data and "requires" in data["build-system"]:
            for item in data["build-system"]["requires"]:
                if isinstance(item, str):
                    dependancies.append(item)
                    print(f"added dependancy {item} from toml")
    except Exception as e:
        print(f"Error parsing pyproject.toml: {e}")
    return None
        


def searchDependenciesInAstObject(item, dependancies):
    string_value = None
    if isinstance(item, ast.Str):  # For Python <3.8
        string_value = item.s
    elif isinstance(item, ast.Constant) and isinstance(item.value, str):
        string_value = item.value
    if string_value:
        dependancies.append(string_value)
        print(f"added dependancy {string_value} from setup.py")
    return None

