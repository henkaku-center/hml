action <- 1:4 # up = 1, down = 2, left = 3, right = 4
pos_r <- 10
neg_r <- -10
no_r <- 0
inv_r <- -1000
goal_r <- 20

learn_rate <- 0.9
gama <- 0.95

init_val <- 0

# qVals <- array(0, dim = c(4, 7, 4))
qVals <- array(0, dim = c(3, 3, 4))
qVals[3, , 1] <- inv_r
qVals[1, , 2] <- inv_r
qVals[ , 1, 3] <- inv_r
qVals[ , 3, 4] <- inv_r

upThresh <- 0.01

max_its <- 20 # each episode ends after 20 time steps

init_s <- c(1, 1)
goal <- c(3, 3)
# goal_s1 <- c(1,1)
# goal_s2 <- c(1,7)

epsVal <- 0.1 # pick max val with pro of 1-epsVal

poss_action <- function(s){
  a <- numeric()
  if (s[1] > 1) {
    a <- c(a, 2)
  } 
  if (s[1] < 3) {
    a <- c(a, 1)
  } 
  if (s[2] > 1) {
    a <- c(a, 3)
  } 
  if (s[2] < 3) {
    a <- c(a, 4)
  } 
  return(a)
}

rm_feedback <- function(s, a){
  fb <- NA
  if (s[1] == 1 & s[2] == 1){
    if (a == 1){
      fb <- no_r
    }else if (a == 4){
      fb <- neg_r
    }else{
      fb <- inv_r
      print('Invalid state and action pair11')
    }
  }else if (s[1] == 2 & s[2] == 1){
    if (a == 1 | a== 2){
      fb <- no_r
    }else if (a == 4){
      fb <- neg_r
    }else{
      fb <- inv_r
      print('Invalid state and action pair21')
    }
  }else if (s[1] == 3 & s[2] == 1){
    if (a == 4 | a == 2){
      fb <- no_r
    }else{
      fb <- inv_r
      print('Invalid state and action pair31')
    }
  }else if (s[1] == 1 & s[2] == 2){
    if (a == 4 | a == 1){
      fb <- neg_r
    }else if (a == 3){
      fb <- no_r
    }else{
      fb <- inv_r
      print('Invalid state and action pair12')
    }
  }else if (s[1] == 2 & s[2] == 2){
    if (a == 4 | a == 2){
      fb <- neg_r
    }else{
      fb <- no_r
    }
  }else if (s[1] == 3 & s[2] == 2){
    if (a == 4){
      fb <- goal_r
    }else if (a == 3){
      fb <- no_r
    }else if (a == 2){
      fb <- neg_r
    }else{
      fb <- inv_r
      print('Invalid state and action pair32')
    }
  }else if (s[1] == 1 & s[2] == 3){
    if (a == 1 | a == 3){
      fb <- neg_r
    }else{
      fb <- inv_r
      print('Invalid state and action pair13')
    }
  }else if (s[1] == 2 & s[2] == 3){
    if (a == 1){
      fb <- goal_r
    }else if (a == 2 | a == 3){
      fb <- neg_r
    }else{
      fb <- inv_r
      print('Invalid state and action pair23')
    }
  }else if (s[1] == 3 & s[2] == 3){
    print('No actions possible from goal (game is over)')
    fb <- no_r
  }else{
    print('Invalid state and action pair33')
  }
  return(fb)
}

af_feedback <- function(s, a){
  fb <- NA
  if (s[1] == 1 & s[2] == 1){
    if (a == 1){
      fb <- pos_r
    }else if (a == 4){
      fb <- neg_r
    }else{
      fb <- inv_r
      print('Invalid state and action pair')
    }
  }else if (s[1] == 2 & s[2] == 1){
    if (a == 1){
      fb <- pos_r
    }else if (a == 2 | a == 4){
      fb <- neg_r
    }else{
      fb <- inv_r
      print('Invalid state and action pair')
    }
  }else if (s[1] == 3 & s[2] == 1){
    if (a == 4){
      fb <- pos_r
    }else if (a == 2){
      fb <- neg_r
    }else{
      fb <- inv_r
      print('Invalid state and action pair')
    }
  }else if (s[1] == 1 & s[2] == 2){
    if (a == 3){
      fb <- pos_r
    }else if (a == 1 | a == 4){
      fb <- neg_r
    }else{
      fb <- inv_r
      print('Invalid state and action pair')
    }
  }else if (s[1] == 2 & s[2] == 2){
    if (a == 4 | a == 2 | a == 3){
      fb <- neg_r
    }else if (a == 1){
      fb <- pos_r
    }else{
      fb <- no_r
    }
  }else if (s[1] == 3 & s[2] == 2){
    if (a == 4){
      fb <- goal_r
    }else if (a == 3 | a == 2){
      fb <- neg_r
    }else{
      fb <- inv_r
      print('Invalid state and action pair')
    }
  }else if (s[1] == 1 & s[2] == 3){
    if (a == 1){
      fb <- pos_r
    }else if (a == 3){
      fb <- neg_r
    }else{
      fb <- inv_r
      print('Invalid state and action pair')
    }
  }else if (s[1] == 2 & s[2] == 3){
    if (a == 1){
      fb <- goal_r
    }else if (a == 2 | a == 3){
      fb <- neg_r
    }else{
      fb <- inv_r
      print('Invalid state and action pair')
    }
  }else if (s[1] == 3 & s[2] == 3){
    print('No actions possible from goal (game is over)')
    fb <- no_r
  }else{
    print('Invalid state and action pair')
  }
  return(fb)
}

act_next <- function(s){
  poss_a <- poss_action(s <- cur_s)
  max_a <- which(qVals[cur_s[1], cur_s[2], poss_a] == max(qVals[cur_s[1], cur_s[2], poss_a]))
  # qVals_next <- qVals[cur_s[1], cur_s[2], ]
  # maxq <- qVals_next[which(qVals_next == max(qVals_next))]
  
  if (runif(1) > epsVal) {
    j <- sample(1:length(max_a), 1)
    act_next <- poss_a[max_a[j]]
  }else{
    non_maxa <- which(qVals[cur_s[1], cur_s[2], poss_a] < max(qVals[cur_s[1], cur_s[2], poss_a]))
    if (length(non_maxa) == 0){
      j <- sample(1:length(max_a), 1)
      act_next <- poss_a[max_a[j]]
    }else{
      j <- sample(1:length(non_maxa), 1)
      act_next <- poss_a[non_maxa[j]]
    }
  }
  return(act_next)
}


sta_next <- function(s, a){
  next_s <- s
  if (a == 1 & s[1] != 3){
    next_s[1] <- s[1] + 1
  }else if (a == 2 & s[1] != 1){
    next_s[1] <- s[1] - 1
  }else if (a == 3 & s[2] != 1){
    next_s[2] <- s[2] - 1
  }else if (a == 4 & s[2] != 3){
    next_s[2] <- s[2] + 1
  }else{
    stop("Invalid action from current state")
  }
  return(next_s)
}

# used to track the training process
# track <- array(NA, dim = c(10000, 20, 4))
# t_track <-1

# update q-values
for (t in 1:10000){
  num_its <- 1
  endP <- FALSE
  cur_s <- init_s
  
  while (endP == FALSE & num_its <= max_its) {
    poss_a <- poss_action(s = cur_s)
    actToTake <- act_next(s = cur_s)
    next_s <- sta_next(s = cur_s, a = actToTake)
    
    #TODO: SWAP based on assignment question number
    # cur_f <- rm_feedback(s = cur_s, a = actToTake)
    cur_f <- af_feedback(s = cur_s, a = actToTake)
    
    next_q_max = max(qVals[next_s[1], next_s[2], ])
    
    #actToTake is current action
    #next_q_max is maximum q-value from next state
    # cur_s and next_s are current state and next state, respectively
    #qVals is 3-d, first two dimensions is first and second dimension of state, third dimension is action 
    #cur_f has feedback for current time step
    # gama is the discount factor
    
    #TODO: FILL ME IN
    pred_err <-  #fill me
      
     qVals[cur_s[1], cur_s[2], actToTake] <- qVals[cur_s[1], cur_s[2], actToTake] + 
      learn_rate*(pred_err)
    cur_s <- next_s
    endP <- cur_s[1] == 3 & cur_s[2] == 3
    num_its <- num_its+1
  }
  # t_track <- t_track + 1
  if (t %% 100 == 0){
    print(paste('------', t, '------' ))
  }
}

table(qVals)
qVals[2,3,]

plotQ <- function(qVals){
  plot(1:3, 1:3, xlim = c(0,3), ylim = c(0,3), xaxt = "n", yaxt = "n", type = "n")
  axis(side = 1, at = 0:3, labels = 0:3)
  axis(side = 2, at = 0:3, labels = 0:3)
  abline(h = 0:3, v = 0:3)

  q_nor <- numeric(length = 8)
  minq <- min(qVals[qVals != min(qVals)])
  maxq <- max(qVals)
  for (i in 1:3){
    for (j in 1:3){
      if (max(qVals[i,j,]) != 0){
        if (length(which(qVals[i,j,] == max(qVals[i,j,]))) == 1){
          mx <- numeric(length = 5)
          mx[1] <- i
          mx[2] <- j
          n_a <- which(qVals[i,j,] == max(qVals[i,j,]))
          mx[3:4] <- sta_next(s = c(i,j), a = n_a)
          mx[5] <- qVals[i,j,which.max(qVals[i,j,])]
          mx[5] <- (mx[5]-minq)/(maxq-minq)
          # s1, s2, s'1, s'2, nor_q
          arrows(x0 = mx[2]-0.5, y0 = mx[1]-0.5,
                 x1 = mx[4]-0.5, y1 = mx[3]-0.5, 
                 lwd = 1, length = 0.05 + 0.3*q_nor[i])
        }else{
          l <- length(which(qVals[i,j,] == max(qVals[i,j,])))
          mx <- matrix(NA, ncol = 6, nrow = l)
          n_a <- which(qVals[i,j,] == max(qVals[i,j,]))
          for (x in 1:l){
            mx[x,1] <- i
            mx[x,2] <- j
            mx[x,3:4] <- sta_next(s = c(i,j), a = n_a[x])
            mx[x,5] <- qVals[i,j,which.max(qVals[i,j,])]
            mx[x,5] <- (mx[x,5]-minq)/(maxq-minq)
            # s1, s2, s'1, s'2, nor_q
            arrows(x0 = mx[x,2]-0.5, y0 = mx[x,1]-0.5,
                   x1 = mx[x,4]-0.5, y1 = mx[x,3]-0.5, 
                   lwd = 1, length = 0.05 + 0.3*q_nor[i])
          }
          
        }
      }
    }
  }
}

plotQ(qVals)


