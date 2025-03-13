from textnode import TextNode, TextType

def main():
    test_var = TextNode("Hello There", TextType.LINK, "https://www.boot.dev")
    print(test_var)

main()
