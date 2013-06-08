#!/usr/bin/ruby
#
#  FieldObj.rb
#  
#
#  Created by Erika Chin.
#  Copyright (c) 2010. All rights reserved.
#
#
#

class FieldObj
attr_accessor :name, :objType, :value, :inClass

def initialize(nam, cls, oType)
	@name="#{cls}.#{nam}"
	@objType=oType
	@inClass = cls
	
	@value=""

end

def getType()
	return @objType
end
def setType(type)
	@objType = type
end


end
