!this program convert a stl file in binary or ascii in a binary format read on amr3d code
!
!Compile it with older gfortran
!
Program stl2amr3d
    implicit none
    character(10)::format_file
    character(400)::input, output
    integer :: num_args, ix

    num_args = command_argument_count()     
    call get_command_argument(1,format_file)      
    call get_command_argument(2,input)      
    call get_command_argument(3,output)      

    ! PRINT*, format_file, input,output, COMMAND_ARGUMENT_COUNT()

    select case(format_file)

    case('ascii')
        call stlascii2amr3d(input,output)
        write(*,*)'The binary file: ',output, 'was created from ascii ', input
    case('binary')
        call stlbinary2amr3d(input,output)
        write(*,*)'The binary file: ',output, 'was created from binary ', input

    end select

end program stl2amr3d
!=======================================================================
subroutine stlascii2amr3d(input,output)
    implicit none
    character(400)::input, output    
    integer:: ib_nlines, ib_np, i
    real*4 n(3),x1(3),x2(3),x3(3)
    character(len=20):: endword, word, i1, i2, i3, i4, i5, i6, i7, i8, i9, actword
    integer:: open_stat1

    word = 'trash'
    endword ='endsolid' 
    endword = trim(endword)
    open(unit=502, file = input, status = 'old')

    ib_nlines=0
    ib_np = 0
    do while (word /= endword)
        read(502,*)word

        if (word == 'facet') ib_np = ib_np + 1  !number of lagrangian points
        ib_nlines = ib_nlines + 1   !line numbers in stl file 
    end do
    close(502)

    open(unit=503, file = input, status = 'old')

    open(unit=504,file=output,form="unformatted",&
        status="unknown",access = "sequential",&
        action="readwrite",iostat=open_stat1)
    if(open_stat1 /= 0) then
        print*, "error during opening of:",output
        stop
    end if

    word ='facet'
    read(503,*)actword
    write(504)ib_np
    do i=1, ib_np
        read(503,*)i1,i2,n(1),n(2),n(3)
        read(503,*)i3,i4
        read(503,*)i5,x1(1),x1(2),x1(3)
        read(503,*)i6,x2(1),x2(2),x2(3)
        read(503,*)i7,x3(1),x3(2),x3(3)
        read(503,*)i8
        read(503,*)i9

        write(504)n(1),n(2),n(3),x1(1),x1(2),x1(3),x2(1),x2(2),x2(3),x3(1),x3(2),x3(3)

    end do

    close(503)  
    close(504)

end subroutine stlascii2amr3d
!=======================================================================
subroutine stlbinary2amr3d(input,output)
    implicit none
    character(400)::input, output  
    real*4 n(3),x1(3),x2(3),x3(3)
    integer*2 padding
    integer*4 ntri,iunit,irc
    integer::i, open_stat1
    character(len=80):: title


    open(unit=504,file=output,form="unformatted",&
        status="unknown",access = "sequential",&
        action="readwrite",iostat=open_stat1)
    if(open_stat1 /= 0) then
        print*, "error during opening of:",output
        stop
    end if


    iunit=505
    open(unit=iunit, file=input,access='direct', form='binary', recl=80)
    read(iunit,rec=1)title
    close(iunit)

    open(unit=iunit, file=input,access='direct', form='binary',recl=4)  
    read(iunit,rec=21)ntri
    close(iunit)

    open(unit=iunit,file=input,access='direct',form='binary',recl=2)
    irc=(80+4)/2+1

    write(504)ntri
    do i=1,ntri

        read(iunit,rec=irc)n(1); irc=irc+2
        read(iunit,rec=irc)n(2); irc=irc+2
        read(iunit,rec=irc)n(3); irc=irc+2

        read(iunit,rec=irc)x1(1); irc=irc+2
        read(iunit,rec=irc)x1(2); irc=irc+2
        read(iunit,rec=irc)x1(3); irc=irc+2

        read(iunit,rec=irc)x2(1); irc=irc+2
        read(iunit,rec=irc)x2(2); irc=irc+2
        read(iunit,rec=irc)x2(3); irc=irc+2

        read(iunit,rec=irc)x3(1); irc=irc+2
        read(iunit,rec=irc)x3(2); irc=irc+2
        read(iunit,rec=irc)x3(3); irc=irc+2

        write(504)n(1),n(2),n(3),x1(1),x1(2),x1(3),x2(1),x2(2),x2(3),x3(1),x3(2),x3(3)

        read(iunit,rec=irc)padding
        irc=irc+1
    end do

    close(iunit)
    close(504)

end subroutine stlbinary2amr3d
!=======================================================================
