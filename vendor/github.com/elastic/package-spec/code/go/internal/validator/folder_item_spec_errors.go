package validator

func adjustErrorDescription(description string) string {
	if description == "Does not match format '" + relativePathFormat + "'" {
		return "relative path is invalid or target doesn't exist"
	}
	return description
}