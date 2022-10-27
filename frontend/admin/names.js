getRequest(`/api/system`, response => {
  const system = JSON.parse(response) 

  const usernames = Array.from(document.getElementsByClassName('username'))
  usernames.forEach(element => element.innerHTML = 'admin')

  const names = Array.from(document.getElementsByClassName('name'))
  names.forEach(element => element.innerHTML = system.name)
})
