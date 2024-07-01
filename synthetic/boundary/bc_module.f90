module bc_module

    use, intrinsic :: iso_fortran_env, only: real64

    implicit none
    save

    logical, private :: module_setup = .false.

    real(kind=real64) :: alpha_bc = 1.0

contains

    subroutine set_bc(data_file)

        implicit none

        character(len=*), optional, intent(in) :: data_file
        integer, parameter :: unit = 13
        character(len=200) :: line

        if (.not.module_setup) then

            ! Open file
            if (present(data_file)) then
                call opendatafile(unit, data_file)
            else
                call opendatafile(unit, 'bc_test.data')
            endif

            read(unit, *) alpha_bc

            close(unit)
            module_setup = .true.

        end if

    end subroutine set_bc

end module bc_module