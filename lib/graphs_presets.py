from types import SimpleNamespace



class GraphAttrPresets:
    
    GraphvizDefault = SimpleNamespace(graph=dict(), group=dict(), node=dict(), edge=dict())
    
    SfgDefault = SimpleNamespace(
        graph=dict(
            rankdir='LR',
        ),
        group=dict(
            shape='rectangle',
            style='filled,rounded',
            color='GreenYellow',
        ),
        node=dict(
            shape='circle',
            style='filled,solid',
            fillcolor='HotPink',
            pencolor='Black',
        ),
        edge=dict(
        ),
    )

    Monochrome = SimpleNamespace(
        graph=dict(
            rankdir='LR',
        ),
        group=dict(
            shape='rectangle',
            style='dashed',
        ),
        node=dict(
            shape='circle',
        ),
        edge=dict(
        ),
    )
