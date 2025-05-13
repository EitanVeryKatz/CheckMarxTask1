 
import os  
import ast  
import toml  

def findDependencyFiles(i_extractPath):  
    """  
    Finds potential dependency files (e.g., setup.py, pyproject.toml, requirements.txt)  
    and metadata files in the extracted package directory.  

    Args:  
        i_extractPath (str): The path to the extracted package directory.  

    Returns:  
        list: A list of dependencies found in the package.  
    """  
    potential_files = {"setup.py", "pyproject.toml", "requirements.txt"}  
    found = {}  
    metadata_path = None  

    for root, dirs, files in os.walk(i_extractPath):  
        for name in potential_files:  
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

    for file_name in potential_files:  
        if file_name not in found:  
            print(f"{file_name} not found")  

    return parseRequirements(found)  


def parseRequirements(i_requirements):  
    """  
    Parses the content of dependency files and extracts dependencies.  

    Args:  
        i_requirements (dict): A dictionary where keys are file names and values are file contents.  

    Returns:  
        list: A list of unique dependencies found in the files.  
    """  
    dependencies = []  

    for file_name, file_content in i_requirements.items():  
        if file_name == "setup.py":  
            ParseSetupPy(file_content, dependencies)  
        elif file_name == "pyproject.toml":  
            parse_pyproject_toml(file_content, dependencies)  
        elif file_name == "requirements.txt":  
            parse_requirements_txt(file_content, dependencies)  
        elif file_name == "METADATA":  
            parse_metadata_file(file_content, dependencies)  

    dependencies = list(set(dependencies))  
    return dependencies  


def parse_requirements_txt(file_content, dependancies):  
    """  
    Parses a requirements.txt file and extracts dependencies.  

    Args:  
        fileContent (str): The content of the requirements.txt file.  
        dependancies (list): A list to store the extracted dependencies.  
    """  
    lines = file_content.splitlines()  
    for line in lines:  
        line = line.strip()  
        if line and not line.startswith("#"):  
            dependancies.append(line)  
            print(f"added dependancy {line} from requirements.txt")  
    return None  


def parse_metadata_file(file_content, dependencies):  
    """  
    Parses a METADATA file and extracts dependencies.  

    Args:  
        fileContent (str): The content of the METADATA file.  
        dependencies (list): A list to store the extracted dependencies.  
    """  
    lines = file_content.splitlines()  
    for line in lines:  
        line = line.strip()  
        if line.startswith("Requires-Dist:"):  
            dep = line[len("Requires-Dist:"):].strip()  
            dependencies.append(dep)  
            print(f"added dependency {dep} from METADATA")  


def ParseSetupPy(i_setupPy, dependancies):  
    """  
    Parses a setup.py file and extracts dependencies using AST (Abstract Syntax Tree).  

    Args:  
        i_setupPy (str): The content of the setup.py file.  
        dependancies (list): A list to store the extracted dependencies.  
    """  
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


def parse_pyproject_toml(path, dependancies):  
    """  
    Parses a pyproject.toml file and extracts dependencies.  

    Args:  
        path (str): The content of the pyproject.toml file.  
        dependancies (list): A list to store the extracted dependencies.  
    """  
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
    """  
    Extracts dependency strings from AST objects.  

    Args:  
        item (ast.AST): The AST object to process.  
        dependancies (list): A list to store the extracted dependencies.  
    """  
    string_value = None  
    if isinstance(item, ast.Str):  
        string_value = item.s  
    elif isinstance(item, ast.Constant) and isinstance(item.value, str):  
        string_value = item.value  
    if string_value:  
        dependancies.append(string_value)  
        print(f"added dependancy {string_value} from setup.py")  
    return None  