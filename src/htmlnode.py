class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"HTMLNode(tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"

    def to_html(self) -> str:
        raise NotImplementedError("Not implemented on HTMLNode")

    def props_to_html(self) -> str:
        props = self.props
        if props is not None and isinstance(props, dict):
            return "".join(list(map(lambda key: f' {key}="{props[key]}"', props)))
        else:
            return ""


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("'value' is required in LeafNode")
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("'tag' is required in ParentNode")
        elif self.children is None or not isinstance(self.children, list):
            raise ValueError(
                "'children' are required in ParentNode (list of HTMLNodes)"
            )
        else:
            return f'<{self.tag}{self.props_to_html()}>{"".join(list(map(lambda x: x.to_html(), self.children)))}</{self.tag}>'
