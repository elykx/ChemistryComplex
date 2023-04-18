def to_representation(data):
    data = data.replace('"', "").replace('"', "")
    rows = data.split('],[')
    rows = [row.replace('[', '').replace(']', '') for row in rows]
    return [list(map(float, row.split(','))) for row in rows]
