from CreateUserProfile import run as createUserProfileRun
from CreateCategory import run as createCategoryRun
from CreateServices import run as createServicesRun
from CreateShortlists import run as createShortlistsRun
from CreateCompletedServices import run as createCompletedServicesRun
from CreateUsers import run as createUsersRun

if __name__ == '__main__':
    createUserProfileRun()
    createCategoryRun()
    createUsersRun()
    createServicesRun()
    createShortlistsRun()
    createCompletedServicesRun()
    
