def triangle_area(base, height):
    return 0.5 * base * height

triangle_base = int(input(""))
triangle_height = int(input(""))
area = triangle_area(triangle_base, triangle_height)
print(f"The area of the triangle with base {triangle_base} and height {triangle_height} is: {area}")