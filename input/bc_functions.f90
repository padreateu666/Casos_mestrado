
! Implement in this file any of the used boundary condition
! functions (use one of the following function names):
!
! - pres property:
!    exact_p
!    dpdx
!    dpdy
!    dpdz
!
! - velu, vu_1, vu_0 properties:
!    exact_u
!    dudx
!    dudy
!    dudz
!    dudt
!
! - velv, vv_1, vv_0 properties:
!    exact_v
!    dvdx
!    dvdy
!    dvdz
!    dvdt
!
! - velw, vw_1, vw_0 properties:
!    exact_w
!    dwdx
!    dwdy
!    dwdz
!    dwdt
!
! - vof property:
!    exact_vof
!
! - sca property:
!    exact_sca
!    dscadx
!    dscady
!    dscadz
!    dscadt
!
! - vari property:
!    exact_var
!    dvardx
!    dvardy
!    dvardz
!    dvardt
!
! - temp property:
!    exact_temp
!    dtempdx
!    dtempdy
!    dtempdz
!    dtempdt
!
! - cond property:
!    exact_cond
!
! - cepe property:
!    exact_cepe
!
! - dens, dens_0, dens_1 properties:
!    exact_rho (if not defined, default is taken from input file)
!
! - visc, visc_0, visc_1 properties:
!    exact_mu (if not defined, default is taken from input file)
!
! - tur1 property:
!    exact_tur1
!    dtur1dx
!    dtur1dy
!    dtur1dz
!    dtur1dt
!
! - tur2 property:
!    exact_tur2
!    dtur2dx
!    dtur2dy
!    dtur2dz
!    dtur2dt
!
! The functions must have the following format:
!
! function <function_name>(t, x, y, z)
!   double precision :: t, x, y, z
!   double precision :: <function_name>
!   
!   !!!!!!!!!!!!!!!!!!!!!!
!   !!! Your Code Here !!!
!   !!!!!!!!!!!!!!!!!!!!!!
!   
!   returnam
! end function <function_ne>

! function exact_u(t,x,y,z)
!     implicit none
!     double precision :: t, x, y, z
!     double precision :: exact_u

!     exact_u = 1d0
! end function exact_u
    
function exact_v(t,x,y,z)
    implicit none
    double precision :: t, x, y, z
    double precision :: exact_v
    double precision :: H,hl,dp,mig,mil,lg,ll
    H = 0.256d0
    hl = 0.02d0
    dp = 0.256d0
    mig = 0.4d0
    mil = 0.8d0
    lg = dp/(0.512d0*mig)
    ll = dp/(0.512d0*mil)
    exact_v = 0.0d0
    if(x>0.0d0 .and. x <= hl ) then
        exact_v = 0*(ll*x*x*0.5d0 + (mig*lg*(hl-H)/mil - ll*hl)*x  )
    endif

    if(x>hl .and. x<H) then
        exact_v = 0*(lg*x*x*0.5d0 - lg*H*x + (mig*lg/mil*(hl-H) - ll*hl*0.5d0)*hl + lg*hl*(H-hl*0.5d0))
    endif
    
end function exact_v


function exact_p(t,x,y,z)
    implicit none

    double precision :: t, x, y, z
    double precision :: exact_p

    exact_p = 1*y
end function exact_p
    
function exact_u(t,x,y,z)
    implicit none
    double precision :: t,x,y,z, exact_u
    exact_u = 0.0d0
end function exact_u