document.write('\\
	<link rel= "stylesheet" type= "text/css" href= "{{ url_for('static',filename='styles/styles.css') }}">
<ul>
          <li><a  class="active"href="{{url_for('instructor')}}">Home</a></li>
          <li><a href="{{url_for('findStudent')}}">Find Student</a></li>
          <li><a href="{{url_for('addStudent')}}">Add Student</a></li>
          <li><a href="{{url_for('testingMonth') }}">Testing Month</a></li>
          <li><a href="{{url_for('qrCode') }}">Quick Login</a></li> 
	  <li><a href="{{url_for('inventory')}}">Inventory</a><li>
 </ul>

	\\');