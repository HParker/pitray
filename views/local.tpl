% for row in albums:
  <h1>{{ item[0] }} </h1>
  
  <p> {{ [item for item in row] }} </p>
% end