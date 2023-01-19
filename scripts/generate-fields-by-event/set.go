// based on the blog from https://www.davidkaya.com/sets-in-golang/
// and the code in https://github.com/deckarep/golang-set
package main

var exists = struct{}{}

type set struct {
    m map[string]struct{}
}

func NewSet() *set {
    s := &set{}
    s.m = make(map[string]struct{})
    return s
}

func (s *set) Add(value string) {
    s.m[value] = exists
}

func (s *set) Remove(value string) {
    delete(s.m, value)
}

func (s *set) Contains(value string) bool {
    _, c := s.m[value]
    return c
}
