import React from 'react';

const UsersList = (props) => {
  return (
		
		<table class="table is-fullwidth has-background-warning" >	
	
			<thead>
                              <tr>                                  
                                  <th class="hidden-xs">ID</th>
                                  <th>Nombre</th>
                                  <th>Email</th>
                                  <th>Direccion</th>
                                  <th>Telefono</th>
                                  <th>Edad</th>
                              </tr>
                          </thead>
      {
        props.users.map((user) => {
          return (								
										<thead>													
												<tr>																		
												  <td>{user.id}</td>
													<td>{user.username}</td>
													<td>{user.email}</td>
													<td>{user.address}</td>
													<td>{user.phone}</td>
													<td>{user.age}</td>
												 </tr>															
											</thead>	
																						
																
          )
				})
				
			}			 									
												
    </table>	
  )
};

export default UsersList;