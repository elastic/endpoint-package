package validator

import (
	"fmt"
	"strings"
)

// ValidationErrors is an error that contains an iterable collection of validation error messages.
type ValidationErrors []error

func (ve ValidationErrors) Error() string {
	if len(ve) == 0 {
		return "found 0 validation errors"
	}

	var message strings.Builder
	errorWord := "errors"
	if len(ve) == 1 {
		errorWord = "error"
	}
	fmt.Fprintf(&message, "found %v validation %v:\n", len(ve), errorWord)
	for idx, err := range ve {
		fmt.Fprintf(&message, "%4d. %v\n", idx+1, err)
	}

	return message.String()
}
