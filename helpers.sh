alias check='./qtest.py $TASK'
alias edit='vim $TASK/$TASK.cpp'
alias trash='mv $TASK/$TASK.cpp{,.old$(date "+%s")} && edit'
alias visualize='python $TASK/visualize.py'
