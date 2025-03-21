
def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line:
            first, rest = line.split(" ", 1)
            if first == "#":
                return(rest.strip())
    raise Exception("No Header in Markdown")
