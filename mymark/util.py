def lines(filetxt):
    '''
    return each line and append a blank line
    '''
    for line in filetxt:
        yield line
    yield '\n'


def blocks(filetxt):
    '''
    return each paragraph, paragraph end with a blank line
    '''
    block = []
    for line in lines(filetxt):
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block = []
