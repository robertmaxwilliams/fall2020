t <- function(p, n, a, b) {
    2*b*log2(p) + a*(n/p - 1 + log2(p))
}
s <- function(p, n, r) {
    r*(n-1)/(2*log2(p) + r*(n/p - 1 + log2(p)))
}
p_opt <- function(n, r) {
    n*r*log(2)/(2+r) 
}

print("optimal p given n=1024 and r=1/3")
print(p_opt(1024, 1/3))
print("corresponding speedup:")
print(s(p_opt(1024, 1/3), 1024, 1/3))
