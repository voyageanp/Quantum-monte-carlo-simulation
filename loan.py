def loan(total, monthly_pay, sum, totalmonth, aftermonth, tmppay):
    totalmonth+=1
    intersest=total*0.021/12
    if monthly_pay - intersest > total:
        print "You totally payed off in ", totalmonth
        sum += total
        print sum
    else:
        totaltmp=0
        if totalmonth == aftermonth:
            totaltmp = total - tmppay
        else:
            totaltmp = total + int(intersest) - monthly_pay
        sum += monthly_pay
        print totaltmp, sum, int(intersest)
        loan(totaltmp, monthly_pay, sum, totalmonth, aftermonth, tmppay)


if __name__ == '__main__':
    loan(1400000, 32700, 0, 0, 4, 0)
