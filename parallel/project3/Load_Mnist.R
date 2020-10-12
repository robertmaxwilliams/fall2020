library(R.utils)
#Load_mnist
# modification of https://gist.github.com/brendano/39760 :
#     Load the MNIST digit recognition dataset into R
#     http://yann.lecun.com/exdb/mnist/
#     assume you have all 4 files and gunzip'd them
#     creates train$n, train$x, train$y  and test$n, test$x, test$y
#     e.g. train$x is a 60000 x 784 matrix, each row is one digit (28x28)
#     call:  show_digit(train$x[5,])   to see a digit.
#     brendan o'connor - gist.github.com/39760 - anyall.org
#
# automatically obtains data from the web
# creates two data frames, test and train
# labels are stored in the y variables of each data frame
# can easily train many models using formula `y ~ .` syntax

#=====================================================================================
# Step 1 download MNIST files and unzip them in the current working directory
#        (use setwd (dir) to change the working directory)
#

# download data from http://yann.lecun.com/exdb/mnist/
download_check = function(url, filename)
{
    if (!file.exists(filename)) {
        download.file(url, filename)
    }
}
download_check("http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz",
              "train-images-idx3-ubyte.gz")
download_check("http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz",
              "train-labels-idx1-ubyte.gz")
download_check("http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz",
              "t10k-images-idx3-ubyte.gz")
download_check("http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz",
              "t10k-labels-idx1-ubyte.gz")


# gunzip the files
try(R.utils::gunzip("train-images-idx3-ubyte.gz"))
try(R.utils::gunzip("train-labels-idx1-ubyte.gz"))
try(R.utils::gunzip("t10k-images-idx3-ubyte.gz"))
try(R.utils::gunzip("t10k-labels-idx1-ubyte.gz"))

library(EBImage)
#============================================================================
# Step 2 Read the MNIST files into datafreames (or Matrices)
#
# Function to load MNIST image files to dataframes
load_image_file = function(filename) 
{
  f = file(filename, 'rb')
  readBin(f, 'integer', n = 1, size = 4, endian = 'big')
  n    = readBin(f, 'integer', n = 1, size = 4, endian = 'big')
  nrow = readBin(f, 'integer', n = 1, size = 4, endian = 'big')
  ncol = readBin(f, 'integer', n = 1, size = 4, endian = 'big')
  x = readBin(f, 'integer', n = n * nrow * ncol, size = 1, signed = FALSE)
  close(f)
  data.frame(matrix(x, ncol = nrow * ncol, byrow = TRUE))
}

# Function to load MNIST label files to vector
load_label_file = function(filename) 
{
  f = file(filename, 'rb')
  readBin(f, 'integer', n = 1, size = 4, endian = 'big')
  n = readBin(f, 'integer', n = 1, size = 4, endian = 'big')
  y = readBin(f, 'integer', n = n, size = 1, signed = FALSE)
  close(f)
  y
}

#==========================================================================
#
#   Explore the MNIST dataset examples
#

# load the image files into the dataframes (train and test)
train = load_image_file("train-images-idx3-ubyte")
str(train)
nrow(train)
View(train)
test  = load_image_file("t10k-images-idx3-ubyte")
nrow(test)

# load labels
train_labels = load_label_file("train-labels-idx1-ubyte")
View(train_labels)
test_labels = load_label_file("t10k-labels-idx1-ubyte")
View(test_labels)
str(test_labels)

# Display train images
n = 1
t = train[n,]  # n-th Image
t = unlist(t, use.names=F) # remove names
mt = matrix(t, nrow = 28, ncol=28) # image pixels are stored row-by-row, top down
display (mt, method="browser")


#===============================================================================
#
#   Read X.bin and Y.bin scripts
#
load_image_bin_file = function(filename, n, nrow, ncol) 
  # Input parameters:
  #   filename        binary file (floats in little endian)
  #   n               number of images
  #   nrow            number of rows per image
  #   ncol            number of columns per image
{
  f = file(filename, 'rb')
  x = readBin(f, 'numeric', n = n * nrow * ncol, size = 4, endian = 'little')
  close(f)
  data.frame(matrix(x, ncol = nrow * ncol, byrow = TRUE))
}

dfX = load_image_bin_file('X.bin', n = 65000, nrow = 28, ncol = 28)
n = 2
t = dfX[n,]  # n-th Image
t = unlist(t, use.names=F) # remove names
mt = matrix(t, nrow = 28, ncol=28) # image pixels are stored row-by-row, top down
display (mt, method="browser")


load_label_bin_file = function(filename, n, numFlotsPerLabel = 10)
  # Input parameters:
  #   filename of binary float labels in little endian
  #   n                     number of labels
  #   numFloatsPerLabel     number of floats used per label
  #
{
  f = file(filename, 'rb')
  y = readBin(f, 'numeric', n = numFlotsPerLabel * n, size = 4, endian = 'little')
  close(f)
  data.frame(matrix(y, ncol = numFlotsPerLabel, byrow = TRUE))
}

Y = load_label_bin_file('Y.bin', n = 65000)
View(Y)













