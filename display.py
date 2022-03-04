# Get parameters related to the table view
def get_view_parms(view_width, columns):
    cell_width, expanded_cells = divmod(view_width, columns)
    cell_width -= 1  # Add space for a pipe character
    cell_template_str = "{{:^{}}}|"
    cell_format_str = cell_template_str.format(cell_width)
    # return {
    #     "cell_width": cell_width,
    #     "expanded_cells": expanded_cells,
    #     "cell_format": cell_format_str
    # }
    return cell_width, expanded_cells, cell_format_str

# Print out the given data. data must be in a two-dimensional list or tuple
def print_data_table(view_parms, data):
    cell_width, expanded_cells, cell_format_str = view_parms
    view_width = len(data[0]) * (cell_width+1) + expanded_cells
    for row in data:
        row = list(map(str, row))  # Just in case the value isn't a string
        longest_text = max(row, key=len)
        lines, extra_line = divmod(len(longest_text), cell_width)
        if extra_line > 0:
            lines += 1

        for line in range(lines):
            extender = expanded_cells
            for col in row:
                start = line * cell_width
                end = start + cell_width
                print(cell_format_str.format(col[start:end]), sep="", end="")
                if extender > 0:
                    print(" ", end="")
                    extender -= 1
            print()  # End of the line
        print("-" * view_width)  # Separator between rows
