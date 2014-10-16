__author__ = 'thorsteinn'

def line_in_file(aLine,file_name):
    '''
    a method for finding if a line in a json.dumps file exits
    :param aLine: a full line of text, not including \m
    :param file_name: the name of a text file, not a reference object
    :return: boolean true if found, false if not found
    '''
    with open(file_name,'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.strip() == aLine.strip():
            return True
    return False

def add_unique_line_to_file(aLine, file_name):
    """
    adds a line to a file if no other identical line exists in the file
    :param aLine: a string that should be added to a textfile
    :param file_name: name of the file
    :return:
    """
    if line_in_file(aLine, file_name) is True:
        return False
    else:
        with open(file_name, 'a') as f:
            f.writelines(aLine + '\n')
    return True

def remove_line_from_file(aLine, file_name):
    if line_in_file(aLine, file_name) is False:
        return False
    else:
        with open(file_name, 'r') as f:
            file_content = f.readlines()
        if aLine in file_content:
            file_content.remove(aLine)
        else:
            file_content.remove(aLine+'\n')

        with open(file_name, 'w') as f:
            f.writelines(file_content)
    return True

