import dst_base
import nexus_file
import nessi_vector

class NeXusDST(dst_base.DST_BASE):
    MIME_TYPE="application/x-NeXus"

    ########## DST_BASE function
    def __init__(self,resource,data_group_path=None,signal=1,so_axis="time_of_flight",
                 *args,**kwargs):

        # allocate places for everything
        self.__nexus=nexus_file.NeXusFile(resource)
        self.__tree=self.__build_tree()
        self.__data_group=None
        self.__data_signal=None
        self.__so_axis=None
        self.__avail_data={}

        # create the data list
        som_ids=self.__generate_SOM_ids()
        for (location,signal) in som_ids:
            data=NeXusData(self.__nexus,self.__tree,location,signal)
            self.__avail_data[(location,signal)]=data

        # set the data group if there is only one
        if data_group_path==None:
            if len(self.__avail_data)==1:
                key=self.__avail_data.keys()[0]
                self.__data_group=key[0]
                self.__signal=key[1]

        # set the so axis
        self.__so_axis=so_axis

    def release_resource(self):
        self.__nexus.close()

    def get_SO_ids(self,SOM_id=None):
        return None

#        change_som= (SOM_id!=None) \
#                    and (SOM_id!=(self.__data_group,self.__data_signal))
#        print "CHANGE:",change_som
#
#        # cache initial state
#        my_data_group=self.__data_group
#        my_data_signal=self.__data_signal
#        my_so_axis=self.__so_axis
#
#        # set the active SOM
#        if change_som:
#            apply(self.set_data,SOM_id)
#
#        print "AXES",self.__so_axis,self.__label_axes
#
#        num_axes=len(self.__data_axes)
#        so_list=[]
#        if num_axes==1:
#            so_list.append(1)
#        elif num_axes==2:
#            pass
#
#        # restore the initial SOM
#        if(change_som):
#            self.set_data(my_data_group,my_data_signal)
#            self.set_SO_axis(my_so_axis)
#
#        return so_list

    def get_SOM_ids(self):
        return self.__avail_data.keys()

    def getSO(self,som_id,so_id):
        return None

    def getSOM(self,som_id=None):
        if(som_id!=None):
            self.set_data((som_id,1))
        return None

    ########## special functions
    def __generate_SOM_ids(self):
        path_list=self.list_type("NXdata")
        SOM_list=[]
        for path in path_list:
            signal_list=self.__get_avail_signals(path)
            for it in signal_list:
                SOM_list.append((path,it))
        return SOM_list

    def __list_level(self):
        listing={}
        self.__nexus.initgroupdir()
        name="blah"
        while name!=None:
            (name,type)=self.__nexus.getnextentry()
            if (name!=None) and (type!="CDF0.0"):
                listing[name]=type
        return listing

    def __prepend_parent(self,parent,listing):
        my_list={}
        for key in listing.keys():
            my_list[("%s/%s" % (parent,key))]=listing[key]
        return my_list

    def __build_tree(self,listing={}):
        # set up result
        my_listing=listing.copy()

        # get a listing for each element in the tree
        if(listing!=None) and (len(listing)>0):
            for parent in listing.keys():
                if(not listing[parent]=="SDS"):
                    self.__nexus.openpath(parent)
                    level_listing=self.__list_level()
                    level_listing=self.__prepend_parent(parent,level_listing)
                    for inner in level_listing.keys():
                        my_listing[inner]=level_listing[inner]
        # or start at the beginning
        else:
            my_listing=self.__prepend_parent("",self.__list_level())

        # recurse if the list has changed
        if len(my_listing)>len(listing):
            return self.__build_tree(my_listing)
        else:
            return my_listing
        
    def __get_data_children(self,data_group=None):
        if(data_group==None):
            data_group=self.__data_group
        if data_group==None:
            return {}

        # get the list of SDS in the data group
        SDS_list=[]
        for key in self.__tree.keys():
            if self.__tree[key]=="SDS":
                if key.startswith(data_group):
                    SDS_list.append(key)

        # create the list of children with attributes
        data_children={}
        for sds in SDS_list:
            data_children[sds]=__get_sds_attr__(self.__nexus,sds)

        return data_children

    def __get_avail_signals(self,data_group):
        children=self.__get_data_children(data_group)

        signal_list=[]
        for child in children.keys():
            for key in children[child]:
                value=children[child][key]
                if key=="signal":
                    signal_list.append(value)

        return signal_list

    def list_type(self,type):
        my_list=[]
        for key in self.__tree.keys():
            if self.__tree[key]==type:
                my_list.append(key)
        return my_list

    def set_SO_axis(self,so_axis):
        data=self.__avail_data[(self.__data_group,self.__data_signal)]
        if data.has_axis(so_axis):
            self.__so_axis=so_axis
        else:
            raise ValueError,"Invalid axis specified (%s)" % so_axis

    def set_data(self,path,signal=1):
        if self.__avail_data.has_key((path,signal)):
            self.__data_group=path
            self.__data_signal=signal
        else:
            raise ValueError,"Invalid data specified (%s,%d)" % (path,signal)

class NeXusData:
    def __init__(self,filehandle,tree,path,signal):
        # do the easy part
        self.location=path
        self.__nexus=filehandle
        self.signal=None
        self.data=None
        self.data_var=None
        self.axes=None
        self.variable=None
        
        # now start pushing through attributes
        children=self.__get_data_children(tree,path)
        axes={}
        for child in children.keys():
            for key in children[child]:
                value=children[child][key]
                if key=="signal": # look for the data
                    if value==signal:
                        self.signal=signal
                        self.data=child
                elif key=="axis": # look for the axis to label themselves
                    axes[value]=NeXusAxis(self.__nexus,child)
        if self.signal==None:
            raise ValueError,"Could not find signal=%d" % int(signal)

        # look for the axes as an attribute to the signal data
        counts_attrlist=children[self.data]
        for key in counts_attrlist.keys():
            if key=="axes":
                inner_list=(counts_attr_list[key]).split(",")
                for i in range(len(inner_list)):
                    axes[i]=NeXusAxis(self.__nexus,inner_list[i])

        # set the axes
        if len(axes)>0:
            self.axes=[]
        for i in range(len(axes)):
            self.axes.append(axes[i+1])
        self.variable=self.axes[0].location

        # if the varience in the counts is not found then set it to be
        # the counts
        if self.data_var==None:
            self.data_var=self.data

    def has_axis(self,axis):
        for my_axis in self.axes:
            if my_axis.label==axis:
                return true
            if my_axis.path==axis:
                return true
        return false

    def __repr__(self,verbose=False):
        result="%s:%d" % (self.location,self.signal)
        if not verbose:
            return result

        for axis in self.axes:
            result=result+"\n  "+str(axis)
        return result

    def __get_data_children(self,tree,data_group=None):
        if data_group==None:
            return {}

        # get the list of SDS in the data group
        SDS_list=[]
        for key in tree.keys():
            if tree[key]=="SDS":
                if key.startswith(data_group):
                    SDS_list.append(key)

        # create the list of children with attributes
        data_children={}
        for sds in SDS_list:
            data_children[sds]=__get_sds_attr__(self.__nexus,sds)

        return data_children

class NeXusAxis:
    def __init__(self,filehandle,path):
        # set the location
        self.location=path

        # the label is the tail of the path
        self.label=path.split("/")[-1]

        # get the value
        filehandle.openpath(path)
        c_axis=filehandle.getdata()
        c_axis_info=filehandle.getinfo()
        self.val=__conv_1d_c2nessi__(filehandle,c_axis,c_axis_info[0],
                                     c_axis_info[1][0])

        # get the list of attributes to set the label and units
        attrs=__get_sds_attr__(filehandle,path)
        try:
            self.units=attrs["units"]
        except KeyError:
            self.units=None
        try:
            self.number=attrs["axis"]
        except KeyError:
            self.number=None


    def __str__(self):
        return "[%d]%s (%s)" % (int(self.number),str(self.label),
                                str(self.units))

def __conv_1d_c2nessi__(filehandle,c_ptr,type,length):
    result=nessi_vector.NessiVector()
    for i in range(length):
        val=nexus_file.get_sds_value(c_ptr,type,i)
        result.append(val)
    return result


def __get_sds_attr__(filehandle,path):
    attrs={}
    filehandle.openpath(path)
    while True:
        (name,value)=filehandle.getnextattr()
        if(name==None): break
        attrs[name]=value
    return attrs

