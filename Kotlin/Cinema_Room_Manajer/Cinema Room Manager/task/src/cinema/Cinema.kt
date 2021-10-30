package cinema


fun showSeats(rows: Int, seats: Int, list: MutableList<MutableList<Int>>) {
    println("\nCinema:")

    print("  ")
    for (i in 1..seats) {
        print("$i ")
    }
    println()
    for (i in 1..rows) {
        print("$i ")
        for (j in 1..seats) {
            val aux = mutableListOf(i, j)
            if (list.contains(aux)) {
                print("B ")
            } else {
                print("S ")
            }
        }
        println()
    }
}

fun menu() {
    println("1. Show the seats")
    println("2. Buy a ticket")
    println("3. Statistics")
    println("0. Exit")
}

fun buyTicket(rows: Int, seats: Int, list: MutableList<MutableList<Int>>, current: MutableList<Int>) {
    var row: Int
    var seat: Int

    do {
        println("\nEnter a row number:")
        row = readLine()!!.toInt()
        println("Enter a seat number in that row:")
        seat = readLine()!!.toInt()

        val aux = mutableListOf(row, seat)

        if (row > rows || seat > seats) {
            println("Wrong input!")
        }
        if (list.contains(aux)) {
            println("That ticket has already been purchased!")
        }
    } while (row > rows || seat > seats || list.contains(aux))

    print("Ticket price: ")

    val price: Int = if (rows * seats > 60) {
            if (row > rows / 2) {
                8
            } else {
                10
            }

        } else {
            10
        }
    println("$$price")
    current.add(price)
    list.add(mutableListOf(row, seat))
}

fun statistics(rows: Int, seats: Int, list: MutableList<MutableList<Int>>, total: Int, current: MutableList<Int>) {
    val aux = list.size * 100.0 / (rows * seats)
    val percentage = String.format("%.2f", aux)

    println("Number of purchased tickets: ${list.size}")
    println("Percentage: $percentage%")
    println("Current income: $${current.sum()}")
    println("Total income: $$total")

}

fun main() {
    println("Enter the number of rows:")
    val rows = readLine()!!.toInt()
    println("Enter the number of seats in each row:")
    val seats = readLine()!!.toInt()
    val list = mutableListOf<MutableList<Int>>()
    val current = mutableListOf<Int>()
    val total = if (rows * seats > 60) {
        (rows / 2) * seats * 10 + ((rows - (rows / 2)) * seats * 8)
    } else {
        rows * seats * 10
    }

    while (true) {
        println()
        menu()
        when (readLine()!!.toInt()) {
            1 -> showSeats(rows, seats, list)
            2 -> buyTicket(rows, seats, list, current)
            3 -> statistics(rows, seats, list, total, current)
            0 -> break
        }
    }

}