package actions

import (
    "net/http"
    
	"github.com/gobuffalo/buffalo"
)

// DashIndex default implementation.
func DashIndex(c buffalo.Context) error {
	return c.Render(http.StatusOK, r.HTML("dash/index.html"))
}

// DashCollections default implementation.
func DashCollections(c buffalo.Context) error {
	return c.Render(http.StatusOK, r.HTML("dash/collections.html"))
}

// DashAccount default implementation.
func DashAccount(c buffalo.Context) error {
	return c.Render(http.StatusOK, r.HTML("dash/account.html"))
}

// DashBrowse default implementation.
func DashBrowse(c buffalo.Context) error {
	return c.Render(http.StatusOK, r.HTML("dash/browse.html"))
}

