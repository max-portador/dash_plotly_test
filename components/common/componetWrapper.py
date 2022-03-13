from dash import html


def componentWrapper(component, title, extra_classes=[]):
    label = html.Span(className='component_wrapper_span', children=[title])
    children = [label, component]
    return html.Div(className=' '.join(['component_wrapper', *extra_classes]),
                    children=children)
