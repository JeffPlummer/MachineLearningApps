from recommendations import critics


def tupleAsHTMLTable(headings, tupleData):
  retString = '<table border="1">'
  retString += "<tr>"
  for h in headings:
    retString += '<th>' + h + '</th>'
  retString += '</tr>'
  
  for tup in tupleData:
    retString += '<tr>'
    for cell in tup:
      retString += '<td>' + str(cell) + '</td>'
    retString += '</tr>'
      
#  for key, value in dictData.items():
#      retString += '<tr><td>' + key + '</td><td>' + value + '</td></tr>'
  retString += '</table>'
  return retString

def criticsAsHTMLTable():
  retString = """<table border="1">
  <tr>
    <th>Person</th>
    <th>Movie</th>
    <th>Rating</th>
  </tr>""";
  for person in critics:
    for movie, rating in critics[person].items():
      retString += '<tr><td>' + person + '</td><td>' + movie + '</td><td>' + str(rating) + '</td></tr>'
  retString += '</table>'
  return retString
