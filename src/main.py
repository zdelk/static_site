from textnode import TextNode, TextType

def main():
    node = TextNode("Hello There", TextType.LINK, "https://www.boot.dev")
    print(node)

main()
