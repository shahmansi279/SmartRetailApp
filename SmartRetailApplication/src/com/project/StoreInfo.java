package com.project;

import android.graphics.Bitmap;
import android.graphics.drawable.Drawable;

public class StoreInfo {

	protected String storeName;
	protected String storeDesc;
	protected Bitmap storebitMap;
	protected String storeUrl;
	protected Drawable plcUrl;
	protected String storeAddr;
	protected String storeId;
	protected String storeTiming;

	public String getStoreTiming() {
		return storeTiming;
	}

	public void setStoreTiming(String storeTiming) {
		this.storeTiming = storeTiming;
	}

	public String getStoreId() {
		return storeId;
	}

	public void setStoreId(String storeId) {
		this.storeId = storeId;
	}

	protected String getStoreAddr() {
		return storeAddr;
	}

	protected void setStoreAddr(String storeAddr) {
		this.storeAddr = storeAddr;
	}

	protected Drawable getPlcUrl() {
		return plcUrl;
	}

	protected void setPlcUrl(Drawable plcUrl) {
		this.plcUrl = plcUrl;
	}

	protected String getStoreName() {
		return storeName;
	}

	protected void setStoreName(String storeName) {
		this.storeName = storeName;
	}

	protected String getStoreDesc() {
		return storeDesc;
	}

	protected void setStoreDesc(String storeDesc) {
		this.storeDesc = storeDesc;
	}

	protected Bitmap getStorebitMap() {
		return storebitMap;
	}

	protected void setStorebitMap(Bitmap storebitMap) {
		this.storebitMap = storebitMap;
	}

	protected String getStoreUrl() {
		return storeUrl;
	}

	protected void setStoreUrl(String storeUrl) {
		this.storeUrl = storeUrl;
	}

}