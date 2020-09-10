for (i=1;i<100;i++)
{
    y[i] = x[i]/c;    // S1
    x[i] = x[i] + c;  // S2
    z[i] = y[i] - c;  // S3
    y[i] = c - y[i];  // S4
}
