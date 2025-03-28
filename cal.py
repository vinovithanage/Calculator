import flet as ft

def main(page: ft.Page):
    page.title = "Flet Calculator"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    
    # State variables
    current_number = ""
    first_number = 0
    operation = ""
    result_shown = False
    
    # Display for the calculator
    result = ft.Text(
        value="0",
        size=40,
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    
    # Update display
    def update_display(value):
        result.value = value
        page.update()
    
    # Handle number button press
    def number_clicked(e):
        nonlocal current_number, result_shown
        number = e.control.text
        
        if result_shown:
            # If we just showed a result, start fresh
            current_number = number
            result_shown = False
        else:
            # Otherwise append to current input
            current_number += number
            
        update_display(current_number)
    
    # Handle operation button press
    def operation_clicked(e):
        nonlocal operation, first_number, current_number, result_shown
        
        if current_number:
            # Save the first number and operation
            first_number = float(current_number)
            operation = e.control.text
            current_number = ""
            update_display(operation)
        elif result.value and result.value not in ["+", "-", "×", "÷"]:
            # Use previous result as first number
            first_number = float(result.value)
            operation = e.control.text
            update_display(operation)
    
    # Calculate the result
    def calculate_result():
        nonlocal first_number, current_number, operation, result_shown
        
        if not current_number or not operation:
            return
        
        second_number = float(current_number)
        result_value = 0
        
        if operation == "+":
            result_value = first_number + second_number
        elif operation == "-":
            result_value = first_number - second_number
        elif operation == "×":
            result_value = first_number * second_number
        elif operation == "÷":
            if second_number == 0:
                update_display("Error")
                return
            result_value = first_number / second_number
        
        # Format result (remove .0 from whole numbers)
        if result_value == int(result_value):
            result_value = int(result_value)
            
        update_display(str(result_value))
        current_number = ""
        operation = ""
        result_shown = True
    
    # Handle equals button press
    def equals_clicked(e):
        calculate_result()
    
    # Handle clear button press
    def clear_clicked(e):
        nonlocal current_number, first_number, operation, result_shown
        current_number = ""
        first_number = 0
        operation = ""
        result_shown = False
        update_display("0")
    
    # Create calculator buttons
    def create_button(text, color, expand=1, on_click=None):
        return ft.ElevatedButton(
            text=text,
            bgcolor=color,
            color=ft.colors.WHITE,
            expand=expand,
            height=60,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=5),
            ),
            on_click=on_click if on_click else number_clicked,
        )
    
    # Set up calculator grid layout
    calculator = ft.Column(
        width=300,
        controls=[
            result,
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
            ft.Row(
                controls=[
                    create_button("C", ft.colors.RED_400, on_click=clear_clicked),
                    create_button("÷", ft.colors.BLUE_400, on_click=operation_clicked),
                ],
            ),
            ft.Row(
                controls=[
                    create_button("7", ft.colors.BLUE_GREY_600),
                    create_button("8", ft.colors.BLUE_GREY_600),
                    create_button("9", ft.colors.BLUE_GREY_600),
                    create_button("×", ft.colors.BLUE_400, on_click=operation_clicked),
                ],
            ),
            ft.Row(
                controls=[
                    create_button("4", ft.colors.BLUE_GREY_600),
                    create_button("5", ft.colors.BLUE_GREY_600),
                    create_button("6", ft.colors.BLUE_GREY_600),
                    create_button("-", ft.colors.BLUE_400, on_click=operation_clicked),
                ],
            ),
            ft.Row(
                controls=[
                    create_button("1", ft.colors.BLUE_GREY_600),
                    create_button("2", ft.colors.BLUE_GREY_600),
                    create_button("3", ft.colors.BLUE_GREY_600),
                    create_button("+", ft.colors.BLUE_400, on_click=operation_clicked),
                ],
            ),
            ft.Row(
                controls=[
                    create_button("0", ft.colors.BLUE_GREY_600, expand=3),
                    create_button("=", ft.colors.ORANGE_400, on_click=equals_clicked),
                ],
            ),
        ],
    )
    
    # Add calculator to the page
    page.add(
        ft.Container(
            content=calculator,
            padding=20,
            border_radius=10,
            bgcolor=ft.colors.BLACK12,
        )
    )

ft.app(target=main)