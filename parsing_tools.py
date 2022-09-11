class Entry:
    # based on https://9elements.com/css-rule-order/
    __position_and_layout = ['position', 'z-index', 'top', 'bottom', 'left', 'right', 'flex-direction', 'flex-wrap', 'flex-flow', 'justify-content', 'align-items', 'align-content', 'order', 'align-self', 'flex-grow', 'flex-shrink', 'flex-basis', 'flex', 'gap', 'grid-auto-rows', 'grid-auto-columns', 'grid-template-rows', 'grid-template-columns', 'grid-row', 'grid-column', 'grid-gap']
    __display_and_visibility = ['display', 'visibility', 'opacity', '-webkit-transform', '-ms-transform', 'transform', 'translate', 'rotate']
    __clipping = ['overflow', 'clip']
    __animation = ['animation', 'transition']
    __box_model = ['margin', 'margin-top', 'margin-right', 'margin-bottom', 'margin-left', 'box-shadow', 'border', 'border-radius', 'border-top-right-radius', 'border-top-left-radius', 'border-bottom-right-radius', 'border-bottom-left-radius', 'box-sizing', 'width', 'height', 'padding', 'padding-top', 'padding-right', 'padding-bottom', 'padding-left']
    __background = ['background', 'background-color', 'background-image', 'background-repeat', 'background-size', 'cursor']
    __typography = ['font-size', 'line-height', 'font-family', 'font-weight', 'font-style', 'text-align', 'text-transform', 'word-spacing', 'color']

    __keys = ['content'] + __position_and_layout + __display_and_visibility + __clipping + __animation + __box_model + __background + __typography

    def __init__(self, content=None):
        self.content = content
        self.props = {}
        self.undefined_props = {}
        if self.content:
            self.__parse_content()

    def __parse_content(self):
        opened_idx = self.content.find('{')
        closed_idx = self.content.rfind('}')
        self.selector = self.content[:opened_idx].strip()
        inner_content = self.content[opened_idx + 1:closed_idx].strip()
        keys_and_vals_str = inner_content.split(';')
        for key_and_val_str in keys_and_vals_str:
            if key_and_val_str.strip():
                key_and_val = key_and_val_str.split(':')
                key = key_and_val[0].strip()
                val = key_and_val[1].strip()
                if key in self.__keys:
                    self.props[key] = val
                else:
                    self.undefined_props[key] = val

    def generate_output(self):
        out_str = self.selector + ' {\n'
        for key in self.__keys:
            if key in self.props:
                out_str += '    ' + key + ': ' + self.props[key] + ';\n' 
        else:
            for undefined_key in self.undefined_props:
                out_str += '    ' + undefined_key + ': ' + self.undefined_props[undefined_key] + ';\n'
        out_str += '}\n\n'
        return out_str

    def get_content(self):
        return self.content

    def get_keys(self):
        return self.__keys

class StyleSheet:
    def __init__(self, source=None):
        self.source = source
        self.entries = []

    def parse(self):
        open_count = 0
        self.entries = []
        closed_idx = 0
        for i in range(len(self.source)):
            if self.source[i] == '{':
                open_count += 1
            elif self.source[i] == '}':
                if open_count == 1:
                    entry = Entry(self.source[:i + 1]) if len(self.entries) == 0 else Entry(self.source[closed_idx + 1:i + 1])
                    closed_idx = i
                    self.entries.append(entry)
                open_count -= 1

    def generate_output(self):
        out_str = ''
        for entry in self.entries:
            out_str += entry.generate_output()
        return out_str
