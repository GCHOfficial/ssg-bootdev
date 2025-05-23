# Static Site Generator

This is the third Boot.dev project, which is a Static Site Generator created using Python.

Designed to generate HTML from Markdown using a node system along with block handling:

- Text is converted to TextNode which has information about the inline Markdown
- TextNode is converted to HTMLNode by transforming the inline Markdown to HTML tags
- Blocks are transformed to HTML in a similar fashion by identifying their type from Markdown and using HTML equivalents

Decent unit testing coverage is done across the main conversion functionality of nodes and blocks, which aided to smoothly progressing through the project and easily identifying issues
