package actions

import (
    "net/http"
    
	"github.com/gobuffalo/buffalo"
)

// UsersLogin default implementation.
func UsersLogin(c buffalo.Context) error {
	return c.Render(http.StatusOK, r.HTML("users/login.html", "front.html"))
}

// UsersRegister default implementation.
func UsersRegister(c buffalo.Context) error {
	return c.Render(http.StatusOK, r.HTML("users/register.html", "front.html"))
}


