from Products.CMFCore.utils import getToolByName

default_profile = 'profile-uwosh.libraryguides:default'

def upgrade(upgrade_product,version):
    """ Decorator for updating the QuickInstaller of a upgrade """
    def wrap_func(fn):
        def wrap_func_args(context,*args):
            p = getToolByName(context,'portal_quickinstaller').get(upgrade_product)
            setattr(p,'installedversion',version)
            return fn(context,*args)
        return wrap_func_args
    return wrap_func


def upgrade_init(context):
    """ Warning """
    print "<<< WARNING >>>"
    print "No upgrade steps before 0.2.3b."

def upgrade_no_change(context):
    """ Default, nothing changes """


@upgrade('uwosh.libraryguides','0.2.0b')
def upgrade_to_0_2_0b(context):
    print "Upgrading"
    
@upgrade('uwosh.libraryguides','0.2.2b')
def upgrade_to_0_2_2b(context):
    print "Upgrading"
    
    
@upgrade('uwosh.libraryguides','0.2.4b')
def upgrade_to_0_2_4b(context):
    print "Upgrading"
    
@upgrade('uwosh.libraryguides','0.2.5b')
def upgrade_to_0_2_5b(context):
    print "Upgrading"
    
@upgrade('uwosh.libraryguides','0.2.6b')
def upgrade_to_0_2_6b(context):
    print "Upgrading"
    
@upgrade('uwosh.libraryguides','0.2.7b')
def upgrade_to_0_2_7b(context):
    print "Upgrading"
    
@upgrade('uwosh.libraryguides','0.2.8b')
def upgrade_to_0_2_8b(context):
    print "Upgrading"
        
@upgrade('uwosh.libraryguides','0.2.9b')
def upgrade_to_0_2_9b(context):
    print "Upgrading"
    
@upgrade('uwosh.libraryguides','0.3.0b')
def upgrade_to_0_3_0b(context):
    print "Upgrading"
    
@upgrade('uwosh.libraryguides','0.3.1b')
def upgrade_to_0_3_1b(context):
    print "Upgrading"
    
@upgrade('uwosh.libraryguides','0.3.2b')
def upgrade_to_0_3_2b(context):
    print "Upgrading"  
    
@upgrade('uwosh.libraryguides','0.3.3b')
def upgrade_to_0_3_3b(context):
    print "Upgrading"  
    
@upgrade('uwosh.libraryguides','0.3.4')
def upgrade_to_0_3_4(context):
    print "Upgrading"  
    
@upgrade('uwosh.libraryguides','0.3.5')
def upgrade_to_0_3_5(context):
    print "Upgrading"  
    
@upgrade('uwosh.libraryguides','0.3.6')
def upgrade_to_0_3_6(context):
    print "Upgrading"  
    
@upgrade('uwosh.libraryguides','0.3.7')
def upgrade_to_0_3_7(context):
    print "Upgrading"  
    
@upgrade('uwosh.libraryguides','0.3.8')
def upgrade_to_0_3_8(context):
    print "Upgrading"  
    
@upgrade('uwosh.libraryguides','0.3.9')
def upgrade_to_0_3_9(context):
    print "Upgrading"  
    
@upgrade('uwosh.libraryguides','0.3.10')
def upgrade_to_0_3_10(context):
    print "Upgrading"  
    
@upgrade('uwosh.libraryguides','0.3.11')
def upgrade_to_0_3_11(context):
    print "Upgrading"  
    
@upgrade('uwosh.libraryguides','0.3.12')
def upgrade_to_0_3_12(context):
    print "Upgrading"  
    
@upgrade('uwosh.libraryguides','0.3.13')
def upgrade_to_0_3_13(context):
    print "Upgrading"  
    
@upgrade('uwosh.libraryguides','0.3.14')
def upgrade_to_0_3_14(context):
    print "Upgrading"  
    
@upgrade('uwosh.libraryguides','0.3.15')
def upgrade_to_0_3_15(context):
    print "Upgrading"  
    
@upgrade('uwosh.libraryguides','0.3.16')
def upgrade_to_0_3_16(context):
    print "Upgrading"  
    
@upgrade('uwosh.libraryguides','0.3.17')
def upgrade_to_0_3_17(context):
    print "Upgrading"  
    
@upgrade('uwosh.libraryguides','0.3.18')
def upgrade_to_0_3_18(context):
    print "Upgrading"
    
@upgrade('uwosh.libraryguides','0.3.19')
def upgrade_to_0_3_19(context):
    print "Upgrading"
    
@upgrade('uwosh.libraryguides','0.3.20')
def upgrade_to_0_3_20(context):
    print "Upgrading"
    
@upgrade('uwosh.libraryguides','0.3.21')
def upgrade_to_0_3_21(context):
    print "Upgrading"
    
@upgrade('uwosh.libraryguides','0.3.22')
def upgrade_to_0_3_22(context):
    context.runImportStepFromProfile(default_profile, 'portlets')
    
@upgrade('uwosh.libraryguides','0.3.23')
def upgrade_to_0_3_23(context):
    print "Upgrading"
    
@upgrade('uwosh.libraryguides','0.3.24')
def upgrade_to_0_3_24(context):
    print "Upgrading"
    
@upgrade('uwosh.libraryguides','0.3.25')
def upgrade_to_0_3_25(context):
    print "Upgrading"
    
@upgrade('uwosh.libraryguides','0.3.26')
def upgrade_to_0_3_26(context):
    print "Upgrading"
    
@upgrade('uwosh.libraryguides','0.3.27')
def upgrade_to_0_3_27(context):
    print "Upgrading"
    
@upgrade('uwosh.libraryguides','0.3.28')
def upgrade_to_0_3_28(context):
    print "Upgrading"
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    